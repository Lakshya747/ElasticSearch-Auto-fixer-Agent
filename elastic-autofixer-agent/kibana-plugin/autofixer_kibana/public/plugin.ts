import { CoreSetup, CoreStart, Plugin } from 'kibana/public';
import { renderApp } from './application';

export class AutofixerKibanaUIPlugin implements Plugin<void, void> {
  public setup(core: CoreSetup) {
    // Register the application in Kibana's registry
    core.application.register({
      id: 'autofixerKibana',
      title: 'Auto-Fixer Agent',
      async mount(context, params) {
        // Mount the React app to the DOM
        const { element } = params;
        const unmount = renderApp(element);
        return () => unmount();
      },
    });
  }

  public start(core: CoreStart) {}
  public stop() {}
}