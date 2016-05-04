import {BaseCountCondition} from './cconditions.base';

export class isEqualCountCondition extends BaseCountCondition{
	type = 'is-equal';
	value: string;

	constructor(options: {
		type?: string,
		point?: number,
		value?: string
	} = {}){
		super(options);
		this.value = options['value'] || '';
	}

	isValid(answer){
		return answer == this.value;
	}

	toPlainObject() {
		let obj = super.toPlainObject();
		obj['value'] = this.value;
		return obj;
	}
}
