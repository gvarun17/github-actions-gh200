const core = require('@actions/core');

// Runs at the end of the job (post step). State comes from core.saveState().
const started = core.getState('started-at');
core.info(`post: greeting step started at ${started || 'unknown'}`);
