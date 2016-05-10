import { Injectable } from '@angular/core';
import { FormBuilder ,ControlGroup } from '@angular/common';
import { QuestionBase } from '../model/question-base';

@Injectable()
export class QuestionControlService {

    constructor(private _fb: FormBuilder) {

    }

    toControlGroup(questions:QuestionBase<any>[]): ControlGroup {
        let group = {};

        questions.forEach(t => group[t.key] = []);

        console.log(group);

        return this._fb.group(group);
    }
}
