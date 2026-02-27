import { IRouter } from 'kibana/server';
import { registerAutofixerRoutes } from './autofixer';

export function defineRoutes(router: IRouter) {
  registerAutofixerRoutes(router);
}