import { BaseConditional } from './condititional-base';
import { QuestionBase } from '../model/question-base';


export class IsEqualConditional extends BaseConditional {
    type = 'is-equal';
    target: QuestionBase<any>;
    value: string;
    constructor(options:{
        target: QuestionBase<any>,
        value: string
    }) {
        super(options);
        this.target = options['target'];
        this.value = options['value'];
    }

    isValid(answers):boolean {
        return answers[this.target.key] == this.value;
    }

    toPlainObject(questions: QuestionBase<any>[]) {
        let obj = super.toPlainObject(questions);
        obj['target'] = questions.indexOf(this.target);
        obj['value'] = this.value;
        return obj;
    }
}
