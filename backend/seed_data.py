import pandas as pd
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, AsyncSessionLocal, Base
from models import Laptop

async def seed():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Load data
    df = pd.read_csv("/laptop.csv", index_col=0)
    
    # Clean data
    df = df.dropna(subset=["price", "ram(GB)", "ssd(GB)", "spec_score", "no_of_cores"])
    
    async with AsyncSessionLocal() as session:
        for _, row in df.iterrows():
            laptop = Laptop(
                model_name=row["model_name"],
                brand=row["brand"],
                price=float(row["price"]),
                ram_gb=int(row["ram(GB)"]),
                ssd_gb=int(row["ssd(GB)"]),
                spec_score=int(row["spec_score"]),
                no_of_cores=int(row["no_of_cores"]),
                is_used=False,
                # Synthetic used price for demo: 70% of new price
                used_price=float(row["price"]) * 0.7 
            )
            session.add(laptop)
        
        await session.commit()
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
