from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from productapp.models import Product
from django.urls import reverse
from commentapp.models import Comment
import requests
# Create your views here



def get_sentiment_and_reply(text):
    try:
        res = requests.post("http://127.0.0.1:5000/predict", json={"text": text})
        if res.status_code == 200:
            data = res.json()
            label = data.get("sentiment")
            
            if "1" in label:
                label = "pos"
            elif "0" in label:
                label = "neg"
            else:
                label = "unknown"

            if label == "pos":
                reply = "ขอบคุณมากค่ะ ทางร้านยินดีที่คุณลูกค้าชอบขนมของเรานะคะ ถ้ามีโอกาสแวะมาอุดหนุนอีก ทางร้านจะตั้งใจทำให้อร่อยเหมือนเดิม ขอบคุณที่สนับสนุนกันนะคะ! 😊"
            elif label == "neg":
                reply = "ทางร้านต้องขออภัยเป็นอย่างสูงสำหรับปัญหาที่เกิดขึ้นค่ะ หวังว่าจะมีโอกาสได้ให้บริการอีกครั้ง และจะพยายามให้ดียิ่งขึ้นค่ะ 🙏"
            else:
                reply = "ขอบคุณสำหรับความคิดเห็นค่ะ"

            return label, reply
    except Exception as e:
        print("[ML ERROR]", e)

    return None, None

@login_required
def add_comment(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        commenttext = request.POST.get('commenttext')
        rating = request.POST.get('rating')

        sentiment, reply = get_sentiment_and_reply(commenttext)

        if commenttext and rating:
            Comment.objects.create(
                user=request.user,
                product=product,
                commenttext=commenttext,
                rating=int(rating),
                sentiment=sentiment,
                reply=reply
            )
        return redirect(reverse('order_history') + '?success=true')
    return redirect(reverse('order_history'))

