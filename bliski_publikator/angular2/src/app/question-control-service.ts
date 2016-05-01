import {Injectable}   from 'angular2/core';
import {ControlGroup, FormBuilder, Validators} from 'angular2/common';
import {QuestionBase} from './model/question-base';

@Injectable()
export class QuestionControlService {
    constructor(private _fb: FormBuilder) { }

    toControlGroup(questions: QuestionBase<any>[]) {
        let group = {};

        questions.forEach(question => {
            group[question.key] = [question.defaultValue || ''];
        });
        return this._fb.group(group);
    }
}
