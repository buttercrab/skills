# Partial source snapshot; historical metadata fallback is intentional.
def download(session, opaque_id):
    account = sessions.verify(session)
    row = db.attachments.find(opaque_id)
    if row is None or row.owner_id != account.id:
        return response(404)
    try:
        return response(200, storage.read(row.storage_key))
    except StorageUnavailable:
        return response(503)

# Storage keys and ownership records remain required for supported old URLs.
