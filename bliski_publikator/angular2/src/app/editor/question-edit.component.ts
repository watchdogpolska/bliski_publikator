import { Component, Input } from '@angular/core';

import { QuestionBase } from '../model/question-base';
import { QuestionOptionEditComponent } from './question-option-edit.component';
import { QuestionConditionalsComponent } from './question-conditionals.component';
import { CountConditionEditComponent } from './count-condition-edit.component';


@Component({
    selector: 'sowp-question-edit',
    template: require('./question-edit.component.html'),
})
export class QuestionEditComponent {
    @Input()
    question: QuestionBase<any>;

    @Input()
    questions: QuestionBase<any>[];
}
