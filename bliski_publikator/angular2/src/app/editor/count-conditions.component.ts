import {
    Component,
    Input
} from '@angular/core';

import { QuestionBase } from '../model/question-base';

import { IsEqualCountCondition } from '../count.conditions/is-equal.cconditions';

@Component({
	'selector': 'sowp-count-conditions',
	'template': require('./count-conditions.component.html')
})
export class CountConditionsComponent {
    @Input()
    current: QuestionBase<any>;

    addIsEqualCondional() {
        let conditions = new IsEqualCountCondition({});
        this.current.countConditions = [
            ...this.current.countConditions,
            conditions
        ];
    }

}
