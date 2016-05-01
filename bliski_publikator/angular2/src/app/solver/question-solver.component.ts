import {
    Component,
    Input,
    OnInit,
    SimpleChange
} from 'angular2/core'
import {
    FormBuilder,
    ControlGroup
} from 'angular2/common'
import { Monitoring } from '../model/monitoring'
import { QuestionBase } from '../model/question-base'
import { QuestionControlService } from './question-control.service'
import { QuestionSolveItemComponent } from './question-solve-item.component'
import { AnswerService } from '../services/answers-api.service';

@Component({
    selector: 'sowp-question-solver',
    template: require('./question-solver.component.html'),
    providers: [
        QuestionControlService,
        AnswerService
    ],
    directives: [
        QuestionSolveItemComponent,
    ]
})
export class QuestionSolverComponent implements OnInit {
    @Input()
    monitoring: Monitoring;

    form: ControlGroup;
    visibility: { key:string, hidden:boolean }[] = [];

    constructor(private _fb: FormBuilder, private _api: AnswerService) {
        console.log(this._fb);
    }

    ngOnInit() {
        this.buildForm();
        console.log(this.form);
        this.form.valueChanges.subscribe((v) => { this.validateVisibility(v) });
        this.validateVisibility(this.form.value);
    }

    private validateVisibility(values){
        let questions = this.monitoring.questions;
        let visibility = [];
        questions.forEach(q => visibility.push({ key: q.key, hidden: q.isHidden(values) }) );
        this.visibility = visibility;
    }
    private buildForm(){
        let group = {}
        this.monitoring.questions.forEach(t => group[t.key] = []);
        this.form = this._fb.group(group);
    }

    onSubmit() {
        let questions = this.monitoring.questions;
        let values = this.form.value;
        let anwers = [];
        for(let answer_key in values){
            var question = questions.find(q => q.key == answer_key);
            anwers.push({ id: question.id, value: values[answer_key] });
        }
        console.log("onSubmit");
        this._api
            .saveAnswers(anwers)
            .subscribe(
                data => { console.log("OK", data) },
                error => { console.log("FAIL", error) }
            );
    }

    isHidden(question: QuestionBase<any>) {
        let o = this.visibility.find(t => t.key == question.key);
        if (!o)
            return false;
        return o.hidden;
    }
}
