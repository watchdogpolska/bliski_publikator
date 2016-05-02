import { Component, Input } from 'angular2/core'
import { ControlGroup } from 'angular2/common';
import { QuestionBase } from '../model/question-base'

@Component({
    selector: 'sowp-question-view',
    template: require('./question-solve-item.component.html'),
})
export class QuestionSolveItemComponent {

    @Input()
    question: QuestionBase<any>

    @Input()
    form: ControlGroup

    constructor() {

    }
}
