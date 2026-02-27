import { PluginInitializerContext } from 'kibana/server'; // Works because of tsconfig paths
import { AutofixerKibanaPlugin } from './plugin';

// This exports the plugin to Kibana
export const plugin = (initializerContext: PluginInitializerContext) => {
  return new AutofixerKibanaPlugin(initializerContext);
};

export { AutofixerKibanaPlugin as Plugin };