import os

class SimpleDocStore:
    def ingest(self, path):
        count = 0
        for filename in os.listdir(path):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_path = os.path.join(path, filename)
                # هنا يمكنك إضافة منطق قراءة الملف أو حفظه في قاعدة بيانات أو أي معالجة أخرى
                print(f"Found file: {file_path}")
                count += 1
        return count

    def ask(self, question):
        # منطق بسيط للإجابة (يمكنك تطويره لاحقاً)
        print(f"Received question: {question}")
        return "لا توجد سياسة استرجاع محددة في النظام حالياً."