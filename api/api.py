
from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from api.exceptions import not_found_exception
from db.models import User, Wallet, Asset
from db.db import get_session
from api.schemas import WalletSchema, AssetSchema, UserSchema


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/users/', response_model=UserSchema)
async def create_user(user: UserSchema, session=Depends(get_session)):
    new_user = User(**user.model_dump())
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return new_user


@router.get('/users/{user_id}', response_model=UserSchema)
async def get_user(user_id: int, session=Depends(get_session)):
    user = await session.get(User, user_id)
    return user


@router.post('/wallets/', response_model=WalletSchema)
async def create_wallet(wallet: WalletSchema, session=Depends(get_session)):
    new_wallet = Wallet(**wallet.model_dump())
    session.add(new_wallet)
    await session.commit()
    await session.refresh(new_wallet)
    return new_wallet


@router.get('/wallets/{wallet_id}', response_model=WalletSchema)
async def get_wallet(wallet_id: int, session=Depends(get_session)):
    wallet = await session.get(Wallet, wallet_id)
    if not wallet:
        return not_found_exception('Wallet')
    return wallet


@router.put('/wallets/{wallet_id}/strategy', response_model=WalletSchema)
async def update_wallet_strategy(wallet_id: int, strategy: dict, session=Depends(get_session)):
    wallet = await session.get(Wallet, wallet_id)
    if not wallet:
        return not_found_exception('Wallet')

    wallet.strategy = strategy
    await session.commit()
    await session.refresh(wallet)
    return wallet


@router.post('/assets/', response_model=AssetSchema)
async def create_asset(asset: AssetSchema, session=Depends(get_session)):
    new_asset = Asset(**asset.model_dump())
    session.add(new_asset)
    await session.commit()
    await session.refresh(new_asset)
    return new_asset


@router.get('/assets/{asset_id}', response_model=AssetSchema)
async def get_asset(asset_id: int, session=Depends(get_session)):
    asset = await session.get(Asset, asset_id)
    if not asset:
        return not_found_exception('Asset')


@router.put('/assets/{asset_id}', response_model=AssetSchema)
async def update_asset(asset_id: int, asset: AssetSchema, session=Depends(get_session)):
    asset = await session.get(Asset, asset_id)
    if not asset:
        return not_found_exception('Asset')
    asset.update(asset.model_dump())
    await session.commit()
    await session.refresh(asset)
    return asset


@router.get('/users/{user_id}/dashboard')
async def get_user_dashboard(request: Request, user_id: int, session=Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        return not_found_exception('User')

    wallet = await session.get(Wallet, user_id)
    if not wallet:
        return not_found_exception('Wallet')

    assets = wallet.assets

    return templates.TemplateResponse("index.html", {
        "request": request,
        "user": user,
        "assets": assets
    })
