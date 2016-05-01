import { BaseConditional } from './condititional-base';
import { QuestionBase } from '../model/question-base';


export class isNullConditional extends BaseConditional{
    type = 'is-null';
    target: QuestionBase<any>;
    constructor(options:{
        target: QuestionBase<any>
    }) {
        super(options)
        this.target = options['target'];
    }

    isValid(answers):boolean {
        return answers[this.target.key] == null || answers[this.target.key] === "";
    }

    toPlainObject(questions: QuestionBase<any>[]) {
        let obj = super.toPlainObject(questions);
        obj['target'] = questions.indexOf(this.target);
        return obj;
    }
}
