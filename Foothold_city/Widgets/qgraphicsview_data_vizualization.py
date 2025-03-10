from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QWheelEvent, QMouseEvent, QPainter


class QGraphicsViewDataVisualization(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        # Параметры масштабирования
        self.zoom_factor = 1.25
        self.min_zoom = 0.1
        self.max_zoom = 10.0

        # Параметры панорамирования
        self.is_panning = False
        self.pan_start = QPointF()
        self.last_mouse_pos = QPointF()

        # Начальные настройки
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        # Важно: разрешаем перехватывать события движения мыши
        self.setMouseTracking(True)

    def wheelEvent(self, event: QWheelEvent) -> None:
        # Обработка зума колесом мыши
        zoom_in = event.angleDelta().y() > 0
        current_zoom = self.transform().m11()

        if zoom_in and current_zoom < self.max_zoom:
            self.scale(self.zoom_factor, self.zoom_factor)
        elif not zoom_in and current_zoom > self.min_zoom:
            self.scale(1 / self.zoom_factor, 1 / self.zoom_factor)

        event.accept()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            # Начало панорамирования
            self.is_panning = True
            self.pan_start = self.mapToScene(event.position().toPoint())
            self.last_mouse_pos = event.position()
            self.setCursor(Qt.CursorShape.ClosedHandCursor)
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self.is_panning:
            # Вычисляем смещение
            delta = event.position() - self.last_mouse_pos
            dx = delta.x()
            dy = delta.y()

            # Преобразуем смещение в координаты сцены
            h_value = self.horizontalScrollBar().value() - dx
            v_value = self.verticalScrollBar().value() - dy

            # Устанавливаем новые значения полос прокрутки
            self.horizontalScrollBar().setValue(h_value)
            self.verticalScrollBar().setValue(v_value)

            self.last_mouse_pos = event.position()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.RightButton:
            # Завершение панорамирования
            self.is_panning = False
            self.setCursor(Qt.CursorShape.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)