import pytest
import os

def test_project_structure():
    assert os.path.exists('src')
    assert os.path.exists('data')
    assert os.path.exists('tests')

def test_requirements():
    assert os.path.exists('requirements.txt')

def test_readme():
    assert os.path.exists('README.md')

def test_ci_workflow():
    assert os.path.exists('.github/workflows/unittests.yml')

def test_imports():
    import pandas
    import numpy
    assert True
