Запуск
```bash
pip install -r requirements.txt
python main.py
```

Чтобы работали клавиши, надо чтобы приложение было активно (поверх всех остальных)
Стрелочки влево\вправо меняют фотографию, вверх\вниз - размер

z\x - меняет сторону экрана

c\v - меняет прозрачность

q или left_ctrl - скрыть фото

esc - выйти полностью

Эти параметры можно менять
```python
images_url = 'https://pastebin.ai/raw/ppkgdvet9s'
opacity = 150
opacity_step = 30
width = 400
width_step = 20
seconds = 30
in_left = True
margin_side = 10
margin_bottom = 100
```
