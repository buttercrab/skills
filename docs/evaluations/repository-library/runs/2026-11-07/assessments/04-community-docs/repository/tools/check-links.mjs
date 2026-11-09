// Local-only check; intentionally no network access.
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
for (const name of readdirSync('docs').filter(name => name.endsWith('.md'))) {
  const file = `docs/${name}`;
  for (const match of readFileSync(file, 'utf8').matchAll(/\]\(([^)#]+)(?:#[^)]*)?\)/g)) {
    const target = match[1];
    if (!/^[a-z]+:/.test(target) && !existsSync(resolve(dirname(file), target))) {
      console.error(`${file}: missing ${target}`);
      process.exitCode = 1;
    }
  }
}
