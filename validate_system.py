#!/usr/bin/env python3
"""
IKMS RAG Feature 4 - System Validation Script
Verifies all components are correctly installed and importable
"""

import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verify Python version compatibility"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✓ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    print(f"✗ Python {version.major}.{version.minor} - Requires 3.8+")
    return False

def check_imports():
    """Verify all critical imports work"""
    imports_to_check = [
        ("langchain", "LangChain core"),
        ("langgraph", "LangGraph (multi-agent)"),
        ("langchain_openai", "LangChain OpenAI"),
        ("pinecone", "Pinecone vector DB"),
        ("fastapi", "FastAPI framework"),
        ("pydantic", "Pydantic models"),
        ("pypdf", "PDF loading"),
        ("dotenv", "Environment variables"),
    ]
    
    print("\n=== Checking Python Imports ===")
    all_ok = True
    for module_name, description in imports_to_check:
        try:
            __import__(module_name)
            print(f"✓ {description:30} - {module_name}")
        except ImportError as e:
            print(f"✗ {description:30} - {module_name}")
            print(f"  Error: {e}")
            all_ok = False
    
    return all_ok

def check_local_modules():
    """Verify local project modules"""
    print("\n=== Checking Project Modules ===")
    
    project_root = Path(__file__).parent
    modules_to_check = [
        ("src.app.models", "Data models"),
        ("src.app.api", "FastAPI application"),
        ("src.app.core.retrieval.vector_store", "Vector store"),
        ("src.app.services.qa_service", "QA service"),
    ]
    
    all_ok = True
    for module_path, description in modules_to_check:
        try:
            parts = module_path.split('.')
            module = __import__(module_path, fromlist=[parts[-1]])
            print(f"✓ {description:30} - {module_path}")
        except (ImportError, ModuleNotFoundError) as e:
            print(f"✗ {description:30} - {module_path}")
            print(f"  Error: {e}")
            all_ok = False
    
    return all_ok

def check_files():
    """Verify critical files exist"""
    print("\n=== Checking Project Files ===")
    
    critical_files = [
        "src/app/api.py",
        "src/app/models.py",
        "src/app/core/retrieval/vector_store.py",
        "src/app/services/qa_service.py",
        "requirements.txt",
        ".env.example",
        "README.md",
    ]
    
    project_root = Path(__file__).parent
    all_ok = True
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - NOT FOUND")
            all_ok = False
    
    return all_ok

def check_environment():
    """Verify environment variables are configured"""
    print("\n=== Checking Environment Setup ===")
    
    required_env = [
        "OPENAI_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT",
        "PINECONE_INDEX_NAME",
    ]
    
    import os
    missing = []
    for var in required_env:
        if os.getenv(var):
            print(f"✓ {var:30} - Set")
        else:
            print(f"⚠ {var:30} - Not set (optional for imports)")
            missing.append(var)
    
    if missing:
        print(f"\nNote: Set these in .env for full functionality:")
        for var in missing:
            print(f"  - {var}")
    
    return True

def main():
    """Run all validation checks"""
    print("\n" + "="*60)
    print("IKMS RAG Feature 4 - System Validation")
    print("="*60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_imports),
        ("Project Modules", check_local_modules),
        ("Project Files", check_files),
        ("Environment", check_environment),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ Error during {name} check:")
            print(f"  {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n✓ All checks passed! System is ready to use.")
        print("\nNext steps:")
        print("  1. Configure .env with your API keys")
        print("  2. Run: uvicorn src.app.api:app --reload")
        print("  3. Open http://localhost:8000/docs for API documentation")
        return 0
    else:
        print("\n✗ Some checks failed. Please review errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
