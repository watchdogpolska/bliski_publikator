import { Component, Input } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { QuestionBase } from '../model/question-base';

@Component({
    selector: 'sowp-solve-item',
    template: require('./solve-item.component.html'),
    // template: './question-solve-item.component.html',
})
export class SolveItemComponent {

    @Input()
    question: QuestionBase<any>;

    @Input()
    form: FormGroup;
}
