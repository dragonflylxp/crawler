import os
import sys
os.environ['CRAWL_PATH'] = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(os.path.join(os.environ['CRAWL_PATH'], 'lib'))
