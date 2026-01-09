# backend/pdf_api.py
from flask import Blueprint, request, jsonify, make_response
import os
import tempfile
import traceback
from datetime import datetime

from backend.commonBackend import (
    get_available_pdf_reports,
    check_pdf_data_availability,
    log_pdf_generation,
    validate_review_number,
    validate_group_id
)
from backend.pdf_generator import generate_review_pdf

pdf_bp = Blueprint("pdf_api", __name__, url_prefix="/pdf")


@pdf_bp.route('/health', methods=['GET'])
def pdf_health_check():
    """Health check endpoint for PDF service"""
    return jsonify({
        'status': 'ok',
        'service': 'pdf_generator',
        'timestamp': datetime.now().isoformat()
    }), 200


@pdf_bp.route('/get-available-pdfs', methods=['GET'])
def get_available_pdfs():
    """
    Fetch all available PDF reports metadata from database
    This doesn't generate PDFs, just returns what can be generated
    """
    try:
        reports = get_available_pdf_reports()
        
        # Add additional metadata
        for report in reports:
            report['can_generate'] = True
            report['pdf_url'] = f"/pdf/generate/{report['review_number']}/{report['group_id']}"
        
        return jsonify({
            'success': True,
            'reports': reports,
            'count': len(reports),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error in get_available_pdfs: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500


@pdf_bp.route('/check-availability/<int:review_number>/<group_id>', methods=['GET'])
def check_pdf_availability(review_number, group_id):
    """
    Check if PDF can be generated for given review and group
    """
    try:
        if not validate_review_number(review_number):
            return jsonify({
                'available': False,
                'error': 'Invalid review number. Must be 1-4.'
            }), 400
        
        if not validate_group_id(group_id):
            return jsonify({
                'available': False,
                'error': 'Invalid group ID format'
            }), 400
        
        result = check_pdf_data_availability(review_number, group_id)
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error checking PDF availability: {e}")
        traceback.print_exc()
        return jsonify({
            'available': False,
            'error': str(e)
        }), 500


@pdf_bp.route('/generate/<int:review_number>/<group_id>', methods=['GET'])
def generate_pdf_on_demand(review_number, group_id):
    """
    Generate PDF on-demand and return as binary stream
    Does NOT save to server permanently
    """
    temp_path = None
    
    try:
        # Validate inputs
        if not validate_review_number(review_number):
            return jsonify({
                'success': False,
                'error': 'Invalid review number. Must be 1-4.'
            }), 400
        
        if not validate_group_id(group_id):
            return jsonify({
                'success': False,
                'error': 'Invalid group ID format'
            }), 400
        
        # Check if data is available
        availability = check_pdf_data_availability(review_number, group_id)
        if not availability.get('available'):
            return jsonify({
                'success': False,
                'error': availability.get('error', 'Required data not available')
            }), 404
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', prefix='review_') as tmp_file:
            temp_path = tmp_file.name
        
        print(f"Generating PDF: Review {review_number}, Group {group_id} -> {temp_path}")
        
        # Generate PDF
        result = generate_review_pdf(review_number, group_id, temp_path)
        
        if not result['success']:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({
                'success': False,
                'error': result.get('error', 'PDF generation failed')
            }), 500
        
        # Read PDF into memory
        with open(temp_path, 'rb') as f:
            pdf_data = f.read()
        
        # Clean up temporary file immediately
        if os.path.exists(temp_path):
            os.remove(temp_path)
            print(f"Cleaned up temp file: {temp_path}")
        
        # Optional: Log generation
        try:
            log_pdf_generation(
                review_number, 
                group_id,
                generated_by=request.remote_addr,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:500]
            )
        except Exception as log_error:
            print(f"Warning: Failed to log PDF generation: {log_error}")
            # Don't fail the request if logging fails
        
        # Create response with PDF
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'inline; filename=Review_{review_number}_{group_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response.headers['Content-Length'] = len(pdf_data)
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        print(f"Successfully generated and sent PDF: {len(pdf_data)} bytes")
        return response
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        traceback.print_exc()
        
        # Clean up temp file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@pdf_bp.route('/download/<int:review_number>/<group_id>', methods=['GET'])
def download_pdf_on_demand(review_number, group_id):
    """
    Generate PDF and force download (same as generate but with attachment disposition)
    """
    temp_path = None
    
    try:
        # Validate inputs
        if not validate_review_number(review_number):
            return jsonify({
                'success': False,
                'error': 'Invalid review number. Must be 1-4.'
            }), 400
        
        if not validate_group_id(group_id):
            return jsonify({
                'success': False,
                'error': 'Invalid group ID format'
            }), 400
        
        # Check if data is available
        availability = check_pdf_data_availability(review_number, group_id)
        if not availability.get('available'):
            return jsonify({
                'success': False,
                'error': availability.get('error', 'Required data not available')
            }), 404
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', prefix='review_') as tmp_file:
            temp_path = tmp_file.name
        
        print(f"Generating PDF for download: Review {review_number}, Group {group_id}")
        
        # Generate PDF
        result = generate_review_pdf(review_number, group_id, temp_path)
        
        if not result['success']:
            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)
            return jsonify({
                'success': False,
                'error': result.get('error', 'PDF generation failed')
            }), 500
        
        # Read PDF into memory
        with open(temp_path, 'rb') as f:
            pdf_data = f.read()
        
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
        
        # Optional: Log generation
        try:
            log_pdf_generation(
                review_number, 
                group_id,
                generated_by=request.remote_addr,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:500]
            )
        except:
            pass
        
        # Create response with PDF (as attachment for download)
        response = make_response(pdf_data)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=Review_{review_number}_{group_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        response.headers['Content-Length'] = len(pdf_data)
        
        return response
        
    except Exception as e:
        print(f"Error downloading PDF: {e}")
        traceback.print_exc()
        
        # Clean up temp file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except:
                pass
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@pdf_bp.route('/batch-generate', methods=['POST'])
def batch_generate_pdfs():
    """
    Generate multiple PDFs at once (returns list of URLs or errors)
    Useful for bulk operations
    """
    try:
        data = request.get_json()
        requests_list = data.get('requests', [])
        
        if not requests_list:
            return jsonify({
                'success': False,
                'error': 'No PDF requests provided'
            }), 400
        
        results = []
        
        for req in requests_list:
            review_number = req.get('review_number')
            group_id = req.get('group_id')
            
            if not validate_review_number(review_number) or not validate_group_id(group_id):
                results.append({
                    'review_number': review_number,
                    'group_id': group_id,
                    'success': False,
                    'error': 'Invalid parameters'
                })
                continue
            
            availability = check_pdf_data_availability(review_number, group_id)
            if availability.get('available'):
                results.append({
                    'review_number': review_number,
                    'group_id': group_id,
                    'success': True,
                    'url': f"/pdf/generate/{review_number}/{group_id}"
                })
            else:
                results.append({
                    'review_number': review_number,
                    'group_id': group_id,
                    'success': False,
                    'error': availability.get('error', 'Data not available')
                })
        
        return jsonify({
            'success': True,
            'results': results,
            'total': len(results),
            'successful': sum(1 for r in results if r['success'])
        }), 200
        
    except Exception as e:
        print(f"Error in batch PDF generation: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@pdf_bp.route('/statistics', methods=['GET'])
def get_pdf_statistics():
    """
    Get statistics about PDF generation
    """
    try:
        from backend.db import get_connection, close_connection
        
        conn = get_connection()
        if not conn:
            return jsonify({
                'success': False,
                'error': 'Database connection failed'
            }), 500
        
        cursor = conn.cursor(dictionary=True)
        
        stats = {
            'total_groups': 0,
            'reviews_by_type': {},
            'recent_generations': []
        }
        
        # Count total groups
        cursor.execute("SELECT COUNT(DISTINCT group_id) as count FROM projects")
        stats['total_groups'] = cursor.fetchone()['count']
        
        # Count reviews by type
        for review_num in range(1, 5):
            cursor.execute(f"SELECT COUNT(*) as count FROM review{review_num}_group_responses")
            stats['reviews_by_type'][f'review_{review_num}'] = cursor.fetchone()['count']
        
        # Get recent generations (if logging table exists)
        try:
            cursor.execute("""
                SELECT review_number, group_id, generated_at, ip_address
                FROM pdf_generation_logs
                ORDER BY generated_at DESC
                LIMIT 10
            """)
            logs = cursor.fetchall()
            for log in logs:
                if log.get('generated_at'):
                    log['generated_at'] = log['generated_at'].isoformat()
            stats['recent_generations'] = logs
        except:
            stats['recent_generations'] = []
        
        close_connection(conn)
        
        return jsonify({
            'success': True,
            'statistics': stats
        }), 200
        
    except Exception as e:
        print(f"Error getting PDF statistics: {e}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500