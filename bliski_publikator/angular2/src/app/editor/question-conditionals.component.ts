

import {
    Component,
    Input
 } from '@angular/core';

import { QuestionBase } from '../model/question-base';

import { IsEqualConditional } from '../conditionals/conditional-is-equal';
import { IsNullConditional } from '../conditionals/conditional-is-null';
import { IsLessConditional } from '../conditionals/conditional-is-less';
import { IsMoreConditional } from '../conditionals/conditional-is-more';

@Component({
    selector: 'sowp-question-conditionals',
    template: require('./question-conditionals.component.html'),
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

    addIsLessCondional() {
        let target = this.questions[0];
        let conditionals = new IsLessConditional({ target: target, value: '0' });
        this.current.hideConditions = [
            ...this.current.hideConditions,
            conditionals
        ];
    }

    addIsMoreCondional() {
        let target = this.questions[0];
        let conditionals = new IsMoreConditional({ target: target, value: '0' });
        this.current.hideConditions = [
            ...this.current.hideConditions,
            conditionals
        ];
    }
}
