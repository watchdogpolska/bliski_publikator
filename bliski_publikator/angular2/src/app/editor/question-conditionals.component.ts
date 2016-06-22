import { DROPDOWN_DIRECTIVES } from 'ng2-bootstrap/ng2-bootstrap';

import {
    Component,
    Input
 } from '@angular/core';

import { QuestionBase } from '../model/question-base';

import { IsEqualConditional } from '../conditionals/conditional-is-equal';
import { IsNullConditional } from '../conditionals/conditional-is-null';

@Component({
    selector: 'sowp-question-conditionals',
    template: require('./question-conditionals.component.html'),
    directives: [
        DROPDOWN_DIRECTIVES
    ]
})
export class QuestionConditionalsComponent {
    @Input()
    questions: QuestionBase<any>[];

    @Input()
    current: QuestionBase<any>;

    addIsEqualCondional() {
        let target = this.questions[0];
        let conditionals = new IsEqualConditional({ target: target, value: '' });
        this.current.hideConditions = [
            ...this.current.hideConditions,
            conditionals
        ];
    }

    addIsNullCondional() {
        let target = this.questions[0];
        let conditionals = new IsNullConditional({ target: target });
        this.current.hideConditions = [
            ...this.current.hideConditions,
            conditionals
        ];
    }
}
