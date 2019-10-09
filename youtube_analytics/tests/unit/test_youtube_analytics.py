import json
import os

from youtube_analytics import youtube_analytics

def test_generate_stats():
    samples_dir = 'youtube_analytics/tests/unit/samples'
    sample_file = os.path.join(samples_dir, 'comment_analysis_result.json')
    with open(sample_file,'r') as f:
        sample = json.load(f)

    result = youtube_analytics.generate_stats(sample['comments'])
    expected_result = {"analyzed_comments":55,"polarity":{"negative":{"amount":26,"percent":0.4727272727272727},"positive":{"amount":29,"percent":0.5272727272727272}}}
    
    assert(result==expected_result)