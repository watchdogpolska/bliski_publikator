import {
    Component,
    Input
} from '@angular/core';

import { QuestionBase } from '../model/question-base';

import { IsEqualCountCondition } from '../count.conditions/is-equal.cconditions';

@Component({
	'selector': 'sowp-count-condition',
	'template': require('./count-condition-edit.component.html')
})
export class CountConditionEditComponent {
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
