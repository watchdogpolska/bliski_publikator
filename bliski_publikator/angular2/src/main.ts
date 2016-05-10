import {enableProdMode} from '@angular/core';
import {bootstrap} from '@angular/platform-browser-dynamic';
import {FORM_PROVIDERS} from '@angular/common';
import {HTTP_PROVIDERS} from '@angular/http';

import {AppComponent} from './app/app.component';

import {CsrfService} from './app/services/csrf.service';

import 'rxjs/Rx';

if ('prod' === ENV) {
  enableProdMode();
}

bootstrap(AppComponent, [
  HTTP_PROVIDERS,
  CsrfService
]);
