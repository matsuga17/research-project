"""
US Corporate Analytics - Setup Script
"""

from setuptools import setup, find_packages
import os

# READMEを読み込み
def read_file(filename):
    """ファイルを読み込む"""
    filepath = os.path.join(os.path.dirname(__file__), filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    return ''

# requirements.txtから依存関係を読み込み
def read_requirements():
    """requirements.txtから依存関係を読み込む"""
    requirements = []
    filepath = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)
    
    return requirements

setup(
    name='us-corporate-analytics',
    version='1.0.0',
    description='米国企業の財務・ガバナンス分析スキル for Claude',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='US Corporate Analytics Team',
    author_email='support@example.com',
    url='https://github.com/your-repo/us-corporate-analytics',
    license='MIT',
    
    # パッケージの検出
    packages=find_packages(exclude=['tests', 'tests.*', 'notebooks', '*.ipynb']),
    
    # Pythonバージョン
    python_requires='>=3.8',
    
    # 依存関係
    install_requires=read_requirements(),
    
    # オプション依存関係
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'jupyter>=1.0.0',
            'black>=23.0.0',
            'flake8>=6.0.0',
        ],
        'academic': [
            'linearmodels>=5.3',
            'arch>=6.2.0',
            'statsmodels>=0.14.0',
        ],
    },
    
    # パッケージデータ
    include_package_data=True,
    package_data={
        '': ['*.yaml', '*.yml', '*.md', '*.txt'],
        'templates': ['*.xlsx', '*.docx', '*.pptx'],
    },
    
    # エントリーポイント（コマンドラインツール）
    entry_points={
        'console_scripts': [
            'us-corporate=quickstart:main',
            'corporate-batch=scripts.batch_collector:main',
        ],
    },
    
    # 分類子
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial :: Investment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    
    # キーワード
    keywords=[
        'finance', 'corporate', 'SEC', 'EDGAR', 'financial analysis',
        'governance', 'Claude AI', 'research', 'analytics'
    ],
    
    # プロジェクトURL
    project_urls={
        'Documentation': 'https://github.com/your-repo/us-corporate-analytics',
        'Source': 'https://github.com/your-repo/us-corporate-analytics',
        'Tracker': 'https://github.com/your-repo/us-corporate-analytics/issues',
    },
)
