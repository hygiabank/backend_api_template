from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "plano" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "nome" VARCHAR(50) NOT NULL UNIQUE,
    "descricao" TEXT NOT NULL
);
        ALTER TABLE "user" ADD "plano_id" INT;
        ALTER TABLE "user" ADD "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" ADD "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP;
        ALTER TABLE "user" ADD CONSTRAINT "fk_user_plano_ca7395fb" FOREIGN KEY ("plano_id") REFERENCES "plano" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP CONSTRAINT "fk_user_plano_ca7395fb";
        ALTER TABLE "user" DROP COLUMN "plano_id";
        ALTER TABLE "user" DROP COLUMN "created_at";
        ALTER TABLE "user" DROP COLUMN "updated_at";
        DROP TABLE IF EXISTS "plano";"""
