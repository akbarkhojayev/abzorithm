#!/bin/bash
set -e

echo "🔧 TOLIQ TUZATISH BOSHLANDI..."
echo ""

cd /home/abz/Desktop/abzorithm

echo "1️⃣ Eski processes o'chirilmoqda..."
pkill -f "python manage.py runserver" 2>/dev/null || true
pkill -f "python3 manage.py runserver" 2>/dev/null || true
sleep 2

echo "2️⃣ Database migrations apply qilinmoqda..."
/usr/local/bin/python manage.py migrate main --no-input 2>/dev/null || echo "⚠️  Migration sozlamasi"

echo "3️⃣ Database tables check qilinmoqda..."
/usr/local/bin/python manage.py dbshell <<EOF 2>/dev/null || true
.tables
EOF

echo "4️⃣ Backend server start qilinmoqda (8001 portida)..."
/usr/local/bin/python manage.py runserver 0.0.0.0:8001 > /tmp/backend.log 2>&1 &
sleep 3

echo "5️⃣ Backend test qilinmoqda..."
if curl -s http://localhost:8001/api/exams/ > /dev/null 2>&1; then
    echo "✅ Backend ishlayapti!"
else
    echo "❌ Backend javob bermayapti"
    echo "Log:"
    tail -20 /tmp/backend.log
    exit 1
fi

echo ""
echo "🎉 HAMASI TAYYOR!"
echo ""
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Admin: http://localhost:8001/admin"
echo "🔌 API: http://localhost:8001/api"
echo ""
echo "📝 Logs: tail -f /tmp/backend.log"
echo ""
