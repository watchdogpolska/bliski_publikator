import { Component, Input, OnInit } from '@angular/core'
import {
    DropdownQuestion,
    DropdownOption
} from '../model/question-dropdown';

@Component({
    selector: 'sowp-question-option-edit',
    template: require('./question-option-edit.component.html')
})
export class QuestionOptionEditComponent implements OnInit{
    constructor() {}

    @Input()
    question: DropdownQuestion;

    options: DropdownOption[] = []

    ngOnInit() {
        this.options = this.question.options;
        this.question.options_changes.subscribe(
            options => this.options = options
        )
    }

    removeOption(option:any){
        let index = this.options.indexOf(option);
        if(index >= 0){
            this.question.options = [
                ...this.options.slice(0, index),
                ...this.options.slice(index + 1)
            ]
        }
    }

    addOption(){
        this.question.options = [
            ...this.options,
            { key: "", value: "" }
        ];
    }
}
