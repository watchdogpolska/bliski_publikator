import {
    Component,
    ElementRef,
    OnInit,
    Input,
    Output,
    EventEmitter,
    OnChanges
} from 'angular2/core';

declare var tinymce: any;

@Component({
    selector: 'tinymce',
    template: `<textarea class="tinyMCE" style="height:300px"></textarea>`
})
export class TinyMceComponent implements OnInit{

    @Input() value: any;
    @Output() valueChange = new EventEmitter();

    elementRef: ElementRef;
    constructor(elementRef: ElementRef) {
        this.elementRef = elementRef;
    }
    ngOnInit() {
        var that = this;
        tinymce.init(
            {
                selector: ".tinyMCE",
                plugins: ["code"],
                menubar: false,
                toolbar: [
                    [
                        "bold",
                        "italic",
                        "underline",
                        "strikethrough",
                        "alignleft",
                        "aligncenter",
                        "alignright",
                        "alignjustify",
                        "styleselect",
                        "bullist",
                        "numlist",
                        "outdent",
                        "indent",
                        "blockquote",
                        "undo",
                        "redo",
                        "subscript",
                        "superscript",
                        "removeformat"
                    ].join(" ")
                    + "| code"
                ],
                setup: (editor) => {
                    let emmiter = () => {
                        that.valueChange.emit(editor.getContent());
                    }
                    editor.on('change', emmiter);
                    editor.on('keyup', emmiter);
                }
            }
        );
    }

}
