import os
import re
import time
import tempfile
import subprocess
from datetime import datetime
from flask import Flask, render_template, request, jsonify
from config import Config

# Set up Flask application with absolute paths
app = Flask(__name__,
           template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),
           static_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'))
app.config.from_object(Config)

def check_rate():
    """Check if request rate is within limits"""
    current_time = datetime.now()
    filename = os.path.join(
        app.config['RATE_LIMIT_DIR'],
        f"{current_time.strftime('%Y.%m.%d.%H')}{(current_time.minute // 10) * 10}.txt"
    )
    
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        try:
            with open(filename, 'r+') as f:
                count = int(f.read().strip() or '0')
                if count > app.config['MAX_REQUESTS_PER_10MIN']:
                    return False
                f.seek(0)
                f.write(str(count + 1))
                f.truncate()
                return True
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write('1')
            return True
    except (OSError, IOError) as e:
        # Log the error but don't block the request if we can't track rate limits
        print(f"Warning: Could not track rate limits: {e}")
        return True

def validate_input(text, input_type='login'):
    """Validate input strings"""
    if input_type == 'login':
        pattern = r'^[0-9a-zA-Z@%._-]+$'
    else:  # password
        pattern = r'^[0-9a-zA-Z@.~!@#$%^&*()_+=\{\}\[\];:\',.?/\\-]+$'
    
    return bool(re.match(pattern, text))

def test_eduroam_config(login, password, auth_type='mschapv2'):
    """Test eduroam configuration with given credentials"""
    
    # Create config file in the system temp directory
    with tempfile.NamedTemporaryFile(mode='w', suffix='.conf', delete=False) as config_file:
        config = f"""network={{
    ssid="eduroam"
    key_mgmt=WPA-EAP
    eap={'PEAP' if auth_type == 'mschapv2' else 'TTLS'}
    identity="{login}"
    anonymous_identity="{login}"
    password="{password}"
    phase2="{'autheap=MSCHAPV2' if auth_type == 'mschapv2' else 'auth=PAP'}"
}}"""
        config_file.write(config)
        config_path = config_file.name

    # Create output file
    output_path = f"{config_path}.out"
    
    try:
        # Run eapol_test command
        cmd = [
            'eapol_test',  # Let the system find it in PATH
            '-c', config_path,
            '-s', app.config['CLIENT_SECRET'],
            '-a', app.config['RADIUS_SERVER']
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Filter out the first line (Reading configuration file...)
        output_lines = (result.stdout + result.stderr).split('\n')
        if output_lines and output_lines[0].startswith('Reading configuration file'):
            filtered_output = '\n'.join(output_lines[1:])
        else:
            filtered_output = result.stdout + result.stderr
        
        with open(output_path, 'w') as f:
            f.write(filtered_output)
            
        success = result.returncode == 0
        return {
            'success': success,
            'config': config,
            'output': filtered_output
        }
            
    finally:
        # Cleanup temp files
        os.unlink(config_path)
        if os.path.exists(output_path):
            os.unlink(output_path)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test_eduroam():
    login = request.args.get('login')
    password = request.args.get('password')
    
    if not login or not password:
        return render_template('index.html')
        
    if not validate_input(login, 'login'):
        return jsonify({'error': f'Invalid character found in login name: {login}'})
        
    if not validate_input(password, 'password'):
        return jsonify({'error': f'Invalid character found in password'})
        
    if not check_rate():
        return jsonify({'error': f'Rate limit exceeded. Maximum {app.config["MAX_REQUESTS_PER_10MIN"]} requests per 10 minutes'})

    # Test both authentication methods
    results = {
        'mschapv2': test_eduroam_config(login, password, 'mschapv2'),
        'pap': test_eduroam_config(login, password, 'pap')
    }
    
    return render_template(
        'results.html',
        login=login,
        results=results
    )

if __name__ == '__main__':
    app.run(debug=True)
