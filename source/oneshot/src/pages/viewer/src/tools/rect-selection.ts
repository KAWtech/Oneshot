import { Events } from '../events';

class RectSelection {

    activate: () => void;
    deactivate: () => void;

    constructor(events: Events, parent: HTMLElement, canvas: HTMLCanvasElement) {
        const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
        svg.id = 'rect-select-svg';
        svg.classList.add('select-svg');

        // create rect element
        const rect = document.createElementNS(svg.namespaceURI, 'rect') as SVGRectElement;
        rect.setAttribute('fill', 'none');
        rect.setAttribute('stroke', '#f60');
        rect.setAttribute('stroke-width', '1');
        rect.setAttribute('stroke-dasharray', '5, 5');

        const start = { x: 0, y: 0 };
        const end = { x: 0, y: 0 };
        let dragId: number | undefined;

        const updateRect = () => {
            const x = Math.min(start.x, end.x);
            const y = Math.min(start.y, end.y);
            const width = Math.abs(start.x - end.x);
            const height = Math.abs(start.y - end.y);

            rect.setAttribute('x', x.toString());
            rect.setAttribute('y', y.toString());
            rect.setAttribute('width', width.toString());
            rect.setAttribute('height', height.toString());
        };

        const pointerdown = (e: PointerEvent) => {
            if (dragId === undefined && (e.pointerType === 'mouse' ? e.button === 0 : e.isPrimary)) {
                e.preventDefault();
                e.stopPropagation();

                dragId = e.pointerId;
                canvas.setPointerCapture(dragId);

                start.x = end.x = e.offsetX;
                start.y = end.y = e.offsetY;

                updateRect();

                svg.style.display = 'inline';
            }
        };

        const pointermove = (e: PointerEvent) => {
            if (e.pointerId === dragId) {
                e.preventDefault();
                e.stopPropagation();

                end.x = e.offsetX;
                end.y = e.offsetY;

                updateRect();
            }
        };

        const pointerup = (e: PointerEvent) => {
            if (e.pointerId === dragId) {
                e.preventDefault();
                e.stopPropagation();

                const w = canvas.clientWidth;
                const h = canvas.clientHeight;

                canvas.releasePointerCapture(dragId);
                dragId = undefined;

                svg.style.display = 'none';

                events.fire('select.rect', e.shiftKey ? 'add' : (e.ctrlKey ? 'remove' : 'set'), {
                    start: { x: Math.min(start.x, end.x) / w, y: Math.min(start.y, end.y) / h },
                    end: { x: Math.max(start.x, end.x) / w, y: Math.max(start.y, end.y) / h },
                });
            }
        };

        this.activate = () => {
            canvas.addEventListener('pointerdown', pointerdown, true);
            canvas.addEventListener('pointermove', pointermove, true);
            canvas.addEventListener('pointerup', pointerup, true);
        };

        this.deactivate = () => {
            canvas.removeEventListener('pointerdown', pointerdown, true);
            canvas.removeEventListener('pointermove', pointermove, true);
            canvas.removeEventListener('pointerup', pointerup, true);
        };

        parent.appendChild(svg);
        svg.appendChild(rect);
    }

    destroy() {

    }
}

export { RectSelection };
