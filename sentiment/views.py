# sentiment/views.py

from django.shortcuts import render
import re

def simple_sentiment_analysis(text):
    """An improved rule-based sentiment analysis function"""
    # Expanded word lists for better accuracy
    positive_words = [
        'good', 'great', 'excellent', 'happy', 'love', 'wonderful', 'best', 'amazing',
        'fantastic', 'terrific', 'outstanding', 'awesome', 'superb', 'brilliant',
        'perfect', 'delightful', 'pleasant', 'joyful', 'excited', 'impressive',
        'beautiful', 'thank', 'thanks', 'helpful', 'positive', 'recommend', 'better',
        'success', 'successful', 'win', 'winning', 'won', 'well', 'nice', 'good'
    ]
    
    negative_words = [
        'bad', 'terrible', 'awful', 'sad', 'hate', 'worst', 'horrible', 'disappointing',
        'poor', 'frustrating', 'disappointed', 'waste', 'useless', 'annoying', 'fail',
        'failed', 'failure', 'problem', 'difficult', 'wrong', 'trouble', 'unfortunately',
        'unhappy', 'unpleasant', 'inferior', 'broken', 'damage', 'negative', 'error'
    ]
    
    # Intensity modifiers
    intensifiers = [
        'very', 'really', 'extremely', 'absolutely', 'completely', 'totally',
        'highly', 'especially', 'particularly', 'utterly', 'quite', 'thoroughly'
    ]
    
    # Clean and normalize text
    text = text.lower()
    words = re.findall(r'\b\w+\b', text)  # Split into words, removing punctuation
    
    # Initialize scores
    positive_score = 0
    negative_score = 0
    intensity_multiplier = 1.0
    
    # Analyze text
    for i, word in enumerate(words):
        # Check for intensifiers
        if word in intensifiers and i < len(words) - 1:
            intensity_multiplier = 1.5
            continue
            
        # Check sentiment and apply intensity
        if word in positive_words:
            positive_score += 1 * intensity_multiplier
        elif word in negative_words:
            negative_score += 1 * intensity_multiplier
            
        # Reset intensity multiplier
        intensity_multiplier = 1.0
    
    # Calculate final sentiment
    total_score = positive_score - negative_score
    confidence = abs(total_score) / (positive_score + negative_score + 1) * 100 if (positive_score + negative_score) > 0 else 50
    
    # Determine sentiment label with confidence
    if total_score > 0:
        return {'label': 'POSITIVE', 'score': min(confidence, 98)}
    elif total_score < 0:
        return {'label': 'NEGATIVE', 'score': min(confidence, 98)}
    else:
        return {'label': 'NEUTRAL', 'score': 50}

def analyze_sentiment(request):
    text = ""
    sentiment_result = None
    confidence = None

    if request.method == 'POST' and 'text' in request.POST:
        text = request.POST.get('text')
        result = simple_sentiment_analysis(text)
        sentiment_result = result['label']
        confidence = result['score']

    return render(request, 'sentiment/index.html', {
        'text': text,
        'result': {
            'sentiment': sentiment_result.lower() if sentiment_result else None,
            'message': f"The sentiment of your text is: {sentiment_result}" if sentiment_result else "",
            'confidence': round(confidence, 1) if confidence is not None else None
        }
    })
