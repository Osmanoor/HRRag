from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

# Store conversation state
conversation_states = {}

# Predefined responses
RESPONSES = {
    "remote_work_policy": """🏠 سياسة العمل عن بعد في شركتنا:

• يمكنك العمل عن بعد لمدة 14 يوم في السنة
• يجب إخطار مديرك المباشر قبل 3 أيام على الأقل
• يتطلب الحضور للمكتب في الاجتماعات المهمة
• يجب الحفاظ على ساعات العمل المعتادة
• توفير تقرير أسبوعي عن المهام المنجزة

هل لديك أي استفسارات أخرى؟ 💼""",
    
    "paid_leave_question": """✅ نعم، فترة العمل عن بعد هي إجازة مدفوعة لمدة 14 يوم.

هل تريد تقديم طلب للعمل عن بعد لهذه المدة؟ 📝""",
    
    "leave_confirmation": """🎉 تم تقديم طلب العمل عن بعد بنجاح!

• رقم الطلب: #WFH-2024-001
• المدة: 14 يوم
• الحالة: بانتظار موافقة المدير

سيتم إشعارك عبر البريد الإلكتروني فور مراجعة طلبك 📧"""
}

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    message = data.get('message', '').strip()
    conversation_id = data.get('conversation_id', 'default')
    
    # Simulate processing time
    time.sleep(1)
    
    # Get current state
    current_state = conversation_states.get(conversation_id, 'initial')
    
    # Process message based on current state and content
    if "سياسة العمل عن بعد" in message:
        conversation_states[conversation_id] = 'asked_policy'
        return jsonify({
            "response": RESPONSES["remote_work_policy"],
            "conversation_id": conversation_id
        })
    
    elif "اجازة مدفوعة" in message and current_state == 'asked_policy':
        conversation_states[conversation_id] = 'asked_paid'
        return jsonify({
            "response": RESPONSES["paid_leave_question"],
            "conversation_id": conversation_id
        })
    
    elif any(word in message.lower() for word in ["نعم", "اجل", "موافق"]) and current_state == 'asked_paid':
        conversation_states[conversation_id] = 'confirmed'
        return jsonify({
            "response": RESPONSES["leave_confirmation"],
            "conversation_id": conversation_id
        })
    
    # Default response
    return jsonify({
        "response": "عذراً، لم أفهم سؤالك. هل يمكنك إعادة صياغته بطريقة أخرى؟ 🤔",
        "conversation_id": conversation_id
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
