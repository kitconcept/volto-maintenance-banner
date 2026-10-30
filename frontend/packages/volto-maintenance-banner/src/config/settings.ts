import type { ConfigType } from '@plone/registry';
import warningSVG from '@plone/volto/icons/warning.svg';

export default function install(config: ConfigType) {
  config.settings.controlPanelsIcons = {
    ...config.settings.controlPanelsIcons,
    'maintenance-banner': warningSVG,
  };
  return config;
}
