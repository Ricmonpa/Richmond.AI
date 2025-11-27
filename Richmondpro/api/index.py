"""
Vercel Serverless Function para el backend del Co-Pilot
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import pathlib

# Agregar el directorio backend al path
backend_path = pathlib.Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

from app import app as fastapi_app

# El handler para Vercel
handler = fastapi_app

