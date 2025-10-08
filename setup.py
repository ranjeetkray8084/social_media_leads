#!/usr/bin/env python3
"""
Setup script for Social Media Lead Generator
Automates the installation and configuration process
"""

import os
import sys
import subprocess
import platform

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def setup_backend():
    """Setup backend environment and dependencies"""
    print("\n🚀 Setting up Backend...")
    
    # Check if we're in the right directory
    if not os.path.exists('backend'):
        print("❌ Backend directory not found. Please run this script from the project root.")
        return False
    
    os.chdir('backend')
    
    # Create virtual environment
    if not run_command('python -m venv venv', 'Creating virtual environment'):
        return False
    
    # Activate virtual environment and install dependencies
    if platform.system() == 'Windows':
        activate_cmd = 'venv\\Scripts\\activate'
        pip_cmd = 'venv\\Scripts\\pip'
    else:
        activate_cmd = 'source venv/bin/activate'
        pip_cmd = 'venv/bin/pip'
    
    # Install requirements
    if not run_command(f'{pip_cmd} install --upgrade pip', 'Upgrading pip'):
        return False
    
    if not run_command(f'{pip_cmd} install -r requirements.txt', 'Installing Python dependencies'):
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('config.env', 'r') as src:
            with open('.env', 'w') as dst:
                dst.write(src.read())
        print("✅ .env file created from config.env")
        print("⚠️  Please edit .env file and add your Gemini API key")
    
    os.chdir('..')
    return True

def setup_frontend():
    """Setup frontend"""
    print("\n🎨 Setting up Frontend...")
    
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found")
        return False
    
    print("✅ Frontend is ready (static HTML)")
    print("📝 To start frontend server:")
    print("   cd frontend && python -m http.server 3000")
    return True

def create_start_scripts():
    """Create start scripts for easy launching"""
    print("\n📜 Creating start scripts...")
    
    # Backend start script
    if platform.system() == 'Windows':
        backend_script = """@echo off
cd backend
call venv\\Scripts\\activate
python app.py
pause"""
        with open('start_backend.bat', 'w') as f:
            f.write(backend_script)
        
        frontend_script = """@echo off
cd frontend
python -m http.server 3000
pause"""
        with open('start_frontend.bat', 'w') as f:
            f.write(frontend_script)
    else:
        backend_script = """#!/bin/bash
cd backend
source venv/bin/activate
python app.py"""
        with open('start_backend.sh', 'w') as f:
            f.write(backend_script)
        os.chmod('start_backend.sh', 0o755)
        
        frontend_script = """#!/bin/bash
cd frontend
python -m http.server 3000"""
        with open('start_frontend.sh', 'w') as f:
            f.write(frontend_script)
        os.chmod('start_frontend.sh', 0o755)
    
    print("✅ Start scripts created")
    return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETED SUCCESSFULLY!")
    print("="*60)
    
    print("\n📋 NEXT STEPS:")
    print("1. Edit backend/.env file and add your Gemini API key:")
    print("   GEMINI_API_KEY=your_actual_api_key_here")
    
    print("\n2. Start the backend server:")
    if platform.system() == 'Windows':
        print("   Run: start_backend.bat")
        print("   Or: cd backend && venv\\Scripts\\activate && python app.py")
    else:
        print("   Run: ./start_backend.sh")
        print("   Or: cd backend && source venv/bin/activate && python app.py")
    
    print("\n3. Start the frontend server (in a new terminal):")
    if platform.system() == 'Windows':
        print("   Run: start_frontend.bat")
        print("   Or: cd frontend && python -m http.server 3000")
    else:
        print("   Run: ./start_frontend.sh")
        print("   Or: cd frontend && python -m http.server 3000")
    
    print("\n4. Open your browser and go to:")
    print("   http://localhost:3000")
    
    print("\n5. Test the connection in the dashboard")
    
    print("\n📚 DOCUMENTATION:")
    print("   - Backend: backend/README.md")
    print("   - Frontend: frontend/README.md")
    print("   - Main: README.md")
    
    print("\n🆘 SUPPORT:")
    print("   - Check troubleshooting section in README.md")
    print("   - Review logs for error messages")
    print("   - Ensure all dependencies are installed")
    
    print("\n🚀 READY TO GENERATE LEADS WITH AI!")

def main():
    """Main setup function"""
    print("🤖 Social Media Lead Generator Setup")
    print("="*50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed")
        sys.exit(1)
    
    # Create start scripts
    if not create_start_scripts():
        print("❌ Script creation failed")
        sys.exit(1)
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()
