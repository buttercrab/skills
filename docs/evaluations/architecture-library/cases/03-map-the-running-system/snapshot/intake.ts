// Source revision 7f12a6b: current default branch snapshot.
export async function upload(req, deps) {
  const blob = await deps.objectStore.put(req.bytes);
  const record = await deps.db.insert({ blobKey: blob.key, status: "pending" });
  await deps.taskQueue.send({ recordId: record.id });
  return { status: 202, id: record.id };
}
export async function status(id, deps) { return deps.db.get(id); }

export async function parseJob(job, deps) {
  const row = await deps.db.get(job.recordId);
  const bytes = await deps.objectStore.get(row.blobKey);
  const parsed = await deps.parser.parse(bytes);
  await deps.db.update(row.id, { status: "ready", text: parsed.text });
}
