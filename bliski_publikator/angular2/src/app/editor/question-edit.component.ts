import { Component, Input } from 'angular2/core'

import { ACCORDION_DIRECTIVES } from 'ng2-bootstrap/ng2-bootstrap';

import { QuestionBase } from '../model/question-base'
import { QuestionOptionEditComponent } from './question-option-edit.component';
import { QuestionConditionalsComponent } from './question-conditionals.component'
import { CountConditionEditComponent } from './count-condition-edit.component'


@Component({
    selector: 'sowp-question-edit',
    template: require('./question-edit.component.html'),
    directives: [
        ACCORDION_DIRECTIVES,
        QuestionOptionEditComponent,
        QuestionConditionalsComponent,
        CountConditionEditComponent
    ]
})
export class QuestionEditComponent{
    @Input()
    question: QuestionBase<any>

    @Input()
    questions: QuestionBase<any>[]

    constructor() {

    }

}
