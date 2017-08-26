import { Component, Input } from '@angular/core';

import { QuestionBase } from '../model/question-base';

@Component({
    selector: 'sowp-question',
    template: require('./question.component.html'),
})
export class QuestionComponent {
    @Input()
    question: QuestionBase<any>;

    @Input()
    questions: QuestionBase<any>[];
}
