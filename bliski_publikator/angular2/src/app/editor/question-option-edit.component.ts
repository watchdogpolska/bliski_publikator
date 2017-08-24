import { Component, Input, OnInit } from '@angular/core';
import {
    DropdownQuestion,
    DropdownOption
} from '../model/question-dropdown';

@Component({
    selector: 'sowp-question-option-edit',
    template: require('./question-option-edit.component.html')
})
export class QuestionOptionEditComponent implements OnInit {
    @Input()
    question: DropdownQuestion;

    ngOnInit() { }

    removeOption(option:any) {
        let index = this.question.options.indexOf(option);
        if (index >= 0) {
            this.question.options = [
                ...this.question.options.slice(0, index),
                ...this.question.options.slice(index + 1)
            ];
        }
    }

    addOption() {
        this.question.options = [
            ...this.question.options,
            { key: '', value: '' }
        ];
    }
}
