# 🎯 PostgreSQL Change Data Capture (CDC) with Python

### Change Data Capture (CDC)

**What it is**: Change Data Capture (CDC) is a technique used to identify and capture changes made to a data source, be it a database, log file, or other forms of data storage.

**❓ Relevance for Data Engineers**:

1. **Real-Time Data Integration**: CDC enables real-time data integration between operational databases and data warehouses or analytics platforms.
2. **Event Sourcing**: It's crucial for architectures like CQRS (Command Query Responsibility Segregation) that rely on an event log.
3. **Audit**: Keep a detailed log of what data changed, useful for compliance and debugging.

### Write-Ahead Logs (WAL)

**What it is**: Write-Ahead Logging (WAL) is a method where changes to data files are written to a separate log before they are committed. In PostgreSQL, the WAL is the sequence of all changes made to the database.

**Relevance for Data Engineers**:

1. **Data Recovery**: WAL helps in recovering data in case of failure.
2. **Replication**: It's the backbone of both physical and logical replication techniques.
3. **Data Synchronization**: Allows for more flexible strategies in keeping distributed databases in sync.

### Why CDC and WAL are relevant together

1. **Fine-Grained Capture**: WAL allows CDC to capture changes at a very granular level.
2. **Performance**: By reading the WAL, you can perform CDC without adding load to the operational database.
3. **Consistency**: Using WAL ensures that you capture every change, maintaining data integrity.

Data engineers find both CDC and WAL critical for building robust, real-time data pipelines, ensuring data integrity and enabling advanced analytics.

<br>

# 1️⃣ Enable Logical Replication on PostgreSQL Source Database


❓ Lookup how to enable logical replication for postgres

<details>
<summary markdown='span'>💡 Solution</summary>


1. Locate the `postgresql.conf` file in  `/etc/postgresql/[version]/main/`

2. Edit `postgresql.conf` to include the following lines:

    ```plaintext
    wal_level = logical
    max_replication_slots = 5
    max_wal_senders = 5
    ```

3. Restart the PostgreSQL service to apply the changes:

    - On Linux:
        ```bash
        sudo systemctl restart postgresql
        ```

</details>

<br>

# 2️⃣ Create a python script to read the WAL

❓ Try to implement `cdc.py` using the doc strings!

<br>

# 3️⃣ Understand the logs

The logs might look a bit cryptic. You can read exactly what they mean in the postgres docs at [this link here](https://www.postgresql.org/docs/15/protocol-logicalrep-message-formats.html).

<br>
