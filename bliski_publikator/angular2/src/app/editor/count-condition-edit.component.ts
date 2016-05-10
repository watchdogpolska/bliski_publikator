import {
    Component,
    Input
} from '@angular/core';

import { QuestionBase } from '../model/question-base';

import {isEqualCountCondition} from '../count.conditions/is-equal.cconditions'

@Component({
	'selector': 'sowp-count-condition';
	'template': require('./count-condition-edit.component.html')
})
export class CountConditionEditComponent{
    @Input()
    current: QuestionBase<any>

    addIsEqualCondional() {
        let conditions = new isEqualCountCondition({});
        this.current.countConditions = [
            ...this.current.countConditions,
            conditions
        ];
    }

}
