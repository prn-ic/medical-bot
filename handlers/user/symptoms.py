from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from database.query.get import get_symptom_causes, get_cause_solutions
from keyboards.keyboards import generate_symptom_keyboard, user_main_keyboard


async def get_data_by_symptom(callback: types.CallbackQuery):
    causes = get_symptom_causes(callback.data
                                .replace('select_symptom ', '')
                                .split('|')[0])

    cause = causes[0]

    keyboard = generate_symptom_keyboard(cause.symptom.id, 0, score=0)

    await callback.message.edit_text(f'• {cause.sign}', reply_markup=keyboard)


async def accept_cause_answer(callback: types.CallbackQuery):
    await respond_answer(callback, 'yes')


async def decline_cause_answer(callback: types.CallbackQuery):
    await respond_answer(callback, 'no')


async def respond_answer(callback: types.CallbackQuery, answer_type: str):

    index = callback.data.replace(f'{answer_type}_cause ', '').split('|')[1]
    score = callback.data.replace(f'{answer_type}_cause ', '').split('|')[2]

    causes = get_symptom_causes(callback.data
                                .replace(f'{answer_type}_cause ', '')
                                .split('|')[0])

    cause = causes[int(index)]

    index = int(index)
    index += 1
    score = int(score)
    if answer_type == 'yes':
        score += cause.cause_score

    solutions = get_cause_solutions(cause.symptom.id)
    solution = check_answer(solutions, score)

    if solution is not None:
        await callback.message.edit_text(f'Возможно, у вас <i>{solution.name}</i>\n\n'
                                         f'<b>Причины: </b>'
                                         f'{solution.indication} \n'
                                         f'<b>Лечение: </b>'
                                         f'{solution.solution}', parse_mode='HTML')

        return

    if index < len(causes):
        keyboard = generate_symptom_keyboard(cause.symptom.id, int(index), int(score))
        next_cause = causes[int(index)]
        await callback.message.edit_text(f'• {next_cause.sign}', reply_markup=keyboard)
    else:
        await callback.message.edit_text('Проблем не обнаружено')


async def cancel_exam(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('↩️ Возвращаемся в меню',
                                  reply_markup=user_main_keyboard, parse_mode='Markdown')


def check_answer(solutions, score):
    for solution in solutions:
        if solution.score == score:
            return solution

    return None


def register_symptom_handler(dp: Dispatcher):
    dp.register_callback_query_handler(get_data_by_symptom,
                                       Text(startswith='select_symptom '))
    dp.register_callback_query_handler(accept_cause_answer,
                                       Text(startswith='yes_cause '))
    dp.register_callback_query_handler(decline_cause_answer,
                                       Text(startswith='no_cause '))
    dp.register_callback_query_handler(cancel_exam,
                                       Text(startswith='cancel_exam'))
