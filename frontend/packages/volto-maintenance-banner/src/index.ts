import type { ConfigType } from '@plone/registry';
import installSettings from './config/settings';
import installSlots from './config/slots';
import './theme/_main.scss';
function applyConfig(config: ConfigType) {
  installSettings(config);
  installSlots(config);
  return config;
}

export default applyConfig;
