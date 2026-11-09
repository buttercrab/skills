# Current illustrative worker; not executable as a standalone module.
def handle(message):
    refund = database.refunds.get(message.refund_id)
    if refund.status == "paid":
        message.ack()
        return
    result = payments.refund(refund.charge_id, refund.amount_minor)
    database.refunds.update(refund.id, status="paid", provider_id=result.id)
    message.ack()

# API handler runs before queue delivery.
def request_refund(charge_id, amount_minor):
    with database.transaction():
        refund = database.refunds.insert(charge_id, amount_minor, status="requested")
    queue.publish({"refund_id": refund.id})
    return refund.id
