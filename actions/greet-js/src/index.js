const core = require('@actions/core');

async function run() {
  try {
    const who = core.getInput('who', { required: true }).trim();
    if (!/^[\w .-]{1,64}$/.test(who)) {
      throw new Error(`Input 'who' has invalid characters or length: ${who}`);
    }
    const shout = core.getBooleanInput('shout');
    let greeting = `Hello, ${who}`;
    if (shout) greeting = greeting.toUpperCase();

    const time = new Date().toISOString();
    core.info(greeting);
    core.debug(`raw INPUT_WHO=${process.env.INPUT_WHO}`);
    core.setOutput('greeting', greeting);
    core.setOutput('time', time);
    core.saveState('started-at', time); // read by post.js

    await core.summary
      .addHeading('Greeting (JavaScript action)')
      .addTable([
        [{ data: 'Field', header: true }, { data: 'Value', header: true }],
        ['who', who],
        ['greeting', greeting],
        ['time', time],
      ])
      .write();
  } catch (err) {
    core.setFailed(err.message);
  }
}

run();
