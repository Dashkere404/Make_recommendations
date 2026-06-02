# Music Recommendation System

Веб-приложение для музыкальных рекомендаций, построенное на основе **content-based recommendation systems**, **Autoencoder embeddings** и **Siamese Neural Networks**.

Проект позволяет искать музыку, сохранять любимые треки, получать персональные рекомендации и находить похожие композиции.

---

## Функциональность

- поиск треков по названию и исполнителю (по всей базе данных)
- добавление треков в избранное для формирования пользовательских предпочтений
- персональные рекомендации "Музыка для вас" на основе Autoencoder embeddings и kNN
- рекомендации похожих треков на основе Siamese Neural Network embeddings и kNN

---

## Как запустить проект

### 1. Клонировать репозиторий

```bash
git clone <repository_url>
cd make_recommendations
```

### 2. Установить зависимости
```
pip install -r requirements.txt
```

### 3. Запустить приложение
```
streamlit run app.py
```

