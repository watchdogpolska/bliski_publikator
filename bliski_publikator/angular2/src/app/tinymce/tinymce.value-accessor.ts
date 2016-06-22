import {
    Component,
    ElementRef,
    OnInit,
    Input,
    Output,
    EventEmitter,
    Renderer
} from '@angular/core';

declare var tinymce: any;

@Component({
    selector: 'tinymce-editor',
    template: `<textarea class="tinyMCE" style="height:300px"></textarea>`
})
export class TinyMceComponent implements OnInit {
    static instance_count: number = 0;

    @Input()
    value: any;

    @Output()
    valueChange = new EventEmitter();

    instance_id: number;

    // element: HTMLTextAreaElement;

    constructor(
        private renderer: Renderer,
        private component_elment: ElementRef) {
        this.instance_id = TinyMceComponent.instance_count++;
    }

    ngOnInit() {
        let element = this.component_elment.nativeElement.firstChild;
        // Generate fake id based on component id
        let generated_id = 'tinymce-instance-' + this.instance_id;
        // Set
        element.id = generated_id;
        // Init TinyMCE
        tinymce.init(
            {
                selector: `#${generated_id}`,
                plugins: ['code'],
                menubar: false,
                toolbar: [
                    [
                        'bold',
                        'italic',
                        'underline',
                        'strikethrough',
                        'alignleft',
                        'aligncenter',
                        'alignright',
                        'alignjustify',
                        'styleselect',
                        'bullist',
                        'numlist',
                        'outdent',
                        'indent',
                        'blockquote',
                        'undo',
                        'redo',
                        'subscript',
                        'superscript',
                        'removeformat'
                    ].join(' ')
                    + '| code'
                ],
                setup: (editor) => {
                    let emmiter = () => {
                        let value = editor.getContent();
                        this.valueChange.emit(value);
                    };
                    editor.on('change', emmiter);
                    editor.on('keyup', emmiter);
                }
            }
        );
    }

}
